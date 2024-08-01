#!/usr/bin/env python3

import os
import json

from MySQLdb import _mysql

from import_gs.load_gs import get_rows

# The ID and range of a sample spreadsheet.
SHEET_ID_REGISTRATION_2024_1ST = '1l7-P4EixDlXfLYBmtkJCsA3XJ8cFLlIjScan5DHvfgc'
SHEET_ID_ATTENDANCE_2024_1ST = '1CqwL_FCyKG_D_9V6pCbT9gKetUgdmB-kGeY1Ue4Cl0k'
RANGE_NAME = "Form Responses 1"


def get_db():
    db = _mysql.connect(
        host=os.environ.get('MYSQL_HOST'),
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        database=os.environ.get('MYSQL_DATABASE')
    )
    return db


def load_google_sheet(sheet_id, range_name, identifier, use_cache=True):
    filename = f'{identifier}.json'
    if use_cache and os.path.isfile(filename):
        with open(filename, 'r') as fr:
            return json.load(fr)

    rows = get_rows(sheet_id, range_name)
    with open(filename, 'w') as fw:
        json.dump(rows, fw)

    return rows


def import_registration():
    rows = load_google_sheet(
        SHEET_ID_REGISTRATION_2024_1ST, RANGE_NAME, 'registration-2024-1st'
    )
    '''
    [0] registered_at TIMESTAMP NOT NULL,
    [1] email VARCHAR(255),
    [2] name_kr VARCHAR(64),
    [3] name_en VARCHAR(128),
    [4] preferred_name VARCHAR(4),
    [5] dob DATE,
    [6] gender TINYINT,
    [7] phone VARCHAR(16),
    [8] kakaotalk VARCHAR(32),
    [9] prefer_college TINYINT,
    [10] note TEXT,
    [11] want_register TINYINT,
    '''
    for row in rows:
        row[4] = 'kr' if row[4] == '한국어 이름' else 'en'
        row[6] = 0 if row[6] == '남자 (Male)' else 1
        try:
            row[9] = 1 if row[9] == 'Yes' else 0
            row[11] = 1 if row[11] == '공동체 등록 원합니다.' else 0
        except IndexError:
            pass

    db = get_db()
    c = db.cursor()
    c.executemany(
        """INSERT INTO registration (
            registered_at, email, name_kr, name_en, preferred_name, dob, gender,
            phone, kakaotalk, prefer_college, note, want_register)
        VALUES (
            %s, %s, %s, %s, %s, %s, %d,
            %s, %s, %d, %s, %d
        )""",
        rows
    )


def import_attendance():
    rows = load_google_sheet(
        SHEET_ID_ATTENDANCE_2024_1ST, RANGE_NAME, 'attendance-2024-1st'
    )
    for row in rows:
        row[1] = row[1].strip().strip('\x08')

    '''
    [0] table_group VARCHAR(32),
    [1] name VARCHAR(255),
    [2] date DATE,
    [3] prayer_request TEXT,
    '''
    db = get_db()
    c = db.cursor()
    c.executemany(
        """INSERT INTO attendance (table_group, name, date, prayer_request)
        VALUES (%s, %s, %s, %s)""",
        rows
    )


def main():
    import_registration()
    import_attendance()


if __name__ == '__main__':
    main()
