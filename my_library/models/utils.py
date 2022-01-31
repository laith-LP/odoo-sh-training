from odoo import fields, _

import csv

DATA_PATH = '/home/laith/odoo-dev/csv-files/library.book.csv'


# TODO: before inserting, pay attention to 1) existence of required fields, 2) their values & constraints.
def scan_file(bk_model):
    """ all_recs read from the file as list of lists, each sublist is a row starting from the header """
    # TODO: validate the file before reading.
    all_recs = read_file()
    header = all_recs[0]
    all_recs.remove(header)

    """ Convert each book to a dictionary """
    recs_as_dicts = convert_recs_into_dicts(all_recs, header)

    """ Before inserting the records, convert each value to the proper format accepted by PSQL """
    inserted_recs_count = 0
    updated_recs_count = 0
    for book_dict in recs_as_dicts:
        ref_id = book_dict['ref_id']
        current_book_rec = bk_model.env['library.book'].search([('ref_id', '=', ref_id)])

        needs_update = False
        if len(current_book_rec) == 1:
            # TODO: use Model.write_date and last_update_date to update based on last update dates.
            needs_update = True
        elif len(current_book_rec) > 1:
            print("More than one book hsa ref_id ->", ref_id)
            continue

        # Since write_date filed is updated automatically by the ORM, remove it from the dictionary.
        book_dict.__delitem__('last_update_date')

        # Get the publisher id that maps to the Publisher's name we got from the csv file, if exists.
        pub_name = book_dict.get('publisher_id')
        pub_id = bk_model.env['res.partner'].search([('name', '=', pub_name)])
        # If it doesn't exist, we may want to create it for the user.
        book_dict['publisher_id'] = int(pub_id[0])

        book_dict['price'] = int(book_dict['price'])

        # Find the key of the state's value.
        state_val = book_dict['state']
        states_list = bk_model.get_state_selection()
        for tup in states_list:
            if tup[0] == state_val or tup[1] == state_val:
                book_dict['state'] = tup[0]
                break

        # Extract the author names from the file then find the corresponding id for each one of them.
        author_names = book_dict['author_ids'].split(',')
        author_ids = []
        for auth_name in author_names:
            auth_id = bk_model.env['res.partner'].search([('name', '=', auth_name)])
            # If the author record doesn't exist, we may want to create it for the user.
            author_ids.append(int(auth_id))
        book_dict['author_ids'] = [[6, False, author_ids]]

        if needs_update:
            update_bk(current_book_rec.id, bk_model, book_dict)
            updated_recs_count += 1
        else:
            bk_model.create(book_dict)
            inserted_recs_count += 1

    print(f"Books Inserted -> {inserted_recs_count}\n"
          f"Books Updated -> {updated_recs_count}")


def read_file():
    all_records = []
    with open(DATA_PATH, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for rec in csv_reader:
            all_records.append(rec)
        csv_file.close()
    return all_records


def convert_recs_into_dicts(all_recs, header):
    recs_as_dicts = []
    columns_count = len(header)
    for rec in all_recs:
        current_rec = {}
        for val_index in range(0, columns_count):
            """
            "" Add key/values pairs:
            "" key   -> header[i]
            "" value -> corresponding value in that field
            """
            header_name = header[val_index]
            current_rec[header_name] = rec[val_index]
        recs_as_dicts.append(current_rec)
    return recs_as_dicts


def update_bk(bk_id, bk_model, vals):
    sql_queries = []

    # {'ref_id': 'A86', 'name': 'Book 113', 'price': 90, 'state': 'coming_soon',
    # 'date_release': '2022-01-21', 'dict_author_ids': [[6, False, [46, 49, 48]]], 'publisher_id': 41}
    cols_and_vals = f"""
        name = '{vals['name']}',
        price = {vals['price']},
        state = '{vals['state']}',
        date_release = '{vals['date_release']}',
        publisher_id = {vals['publisher_id']}
    """
    update_rec_sql = f"""
        UPDATE library_book
            SET {cols_and_vals}
            WHERE id = '{bk_id}'
    """
    sql_queries.append(update_rec_sql)

    bk_model.env.cr.execute(f"""
    SELECT res_partner_id FROM library_book_res_partner_rel
    WHERE library_book_id = {bk_id}""")

    dict_author_ids = vals['author_ids'][0][2]
    db_author_ids = []
    for db_author_id_tup in bk_model.env.cr.fetchall():
        for db_author_id in db_author_id_tup:
            db_author_ids.append(db_author_id)
            if db_author_id not in dict_author_ids:
                sql_queries.append(get_delete_author_sql(bk_id, db_author_id))

    for dict_author_id in dict_author_ids:
        if dict_author_id not in db_author_ids:
            sql_queries.append(get_insert_author_sql(bk_id, dict_author_id))

    for query in sql_queries:
        bk_model.env.cr.execute(query)


def get_delete_author_sql(bk_id, author_id):
    return f"""
        DELETE FROM library_book_res_partner_rel
        WHERE library_book_id = {bk_id} and res_partner_id = {author_id}
    """


def get_insert_author_sql(bk_id, author_id):
    return f"""
        INSERT INTO library_book_res_partner_rel
        VALUES ('{bk_id}', '{author_id}')
    """