# app/models/auto_page_builder.py
from typing import List
from app.database.old_connection import execute_query, execute_insert, start_transaction, commit_transaction, rollback_transaction

def get_page_by_id(page_id: str) -> bool:
    query = "SELECT 1 FROM auto_page_builder WHERE id = %s"
    result = execute_query(query, (page_id,))
    return len(result) > 0

def get_page_by_name(modelName: str) -> dict:
    query = "SELECT * FROM auto_page_builder WHERE modelName = %s"
    result = execute_query(query, (modelName,))
    return result[0] if result else None

def page_exists(modelName: str) -> bool:
    query = "SELECT 1 FROM auto_page_builder WHERE modelName = %s"
    result = execute_query(query, (modelName,))
    return len(result) > 0

def store_page(auto_page_data):
    fields = auto_page_data.fields
    action_labels = auto_page_data.actionLabels
    headers = auto_page_data.headers
    
    cnx = start_transaction()
    try:
        # Insert main auto_page_builder entry
        query = "INSERT INTO auto_page_builder (modelName, modelUri, apiEndpoint) VALUES (%s, %s, %s)"
        execute_insert(query, (auto_page_data.modelName, auto_page_data.modelURI, auto_page_data.apiEndpoint))
        
        # Get the last inserted page id
        page = get_page_by_name(auto_page_data.modelName)
        page_id = page['id']

        
        # Insert fields, action_labels, and headers
        for field in fields:
            query = """
                INSERT INTO auto_page_builder_fields
                (auto_page_builder_id, name, type, label, isRequired, dataType, defaultValue)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            execute_insert(query, (page_id, field.name, field.type, field.label, field.isRequired, field.dataType, field.defaultValue))
    
        for action_label in action_labels:
            query = """
                INSERT INTO auto_page_builder_action_labels
                (auto_page_builder_id, `key`, label, actionType, `show`)
                VALUES (%s, %s, %s, %s, %s)
            """
            execute_insert(query, (page_id, action_label.key, action_label.label, action_label.actionType, action_label.show))
    
        for header in headers:
            query = """
                INSERT INTO auto_page_builder_headers
                (auto_page_builder_id, `key`, label, isVisibleInList, isVisibleInSingleView)
                VALUES (%s, %s, %s, %s, %s)
            """
            execute_insert(query, (page_id, header.key, header.label, header.isVisibleInList, header.isVisibleInSingleView))
        
        commit_transaction(cnx)
    except Exception as e:
        rollback_transaction(cnx)
        raise e

def update_page(page_id: int, auto_page_data):
    fields = auto_page_data.fields
    action_labels = auto_page_data.actionLabels
    headers = auto_page_data.headers
    
    cnx = start_transaction()
    try:
        # Update main auto_page_builder table
        query = """
            UPDATE auto_page_builder
            SET modelName = %s, modelUri = %s, apiEndpoint = %s
            WHERE id = %s
        """
        execute_insert(query, (auto_page_data.modelName, auto_page_data.modelURI, auto_page_data.apiEndpoint, page_id))
        
        # Clear existing fields, action_labels, headers associated with this page_id
        query = "DELETE FROM auto_page_builder_fields WHERE auto_page_builder_id = %s"
        execute_query(query, (page_id,))
        
        query = "DELETE FROM auto_page_builder_action_labels WHERE auto_page_builder_id = %s"
        execute_query(query, (page_id,))
        
        query = "DELETE FROM auto_page_builder_headers WHERE auto_page_builder_id = %s"
        execute_query(query, (page_id,))
        
        # Insert updated fields, action_labels, headers
        for field in fields:
            query = """
                INSERT INTO auto_page_builder_fields
                (auto_page_builder_id, name, type, label, isRequired, dataType, defaultValue)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            execute_insert(query, (page_id, field.name, field.type, field.label, field.isRequired, field.dataType, field.defaultValue))
    
        for action_label in action_labels:
            query = """
                INSERT INTO auto_page_builder_action_labels
                (auto_page_builder_id, `key`, label, actionType, `show`)
                VALUES (%s, %s, %s, %s, %s)
            """
            execute_insert(query, (page_id, action_label.key, action_label.label, action_label.actionType, action_label.show))
    
        for header in headers:
            query = """
                INSERT INTO auto_page_builder_headers
                (auto_page_builder_id, `key`, label, isVisibleInList, isVisibleInSingleView)
                VALUES (%s, %s, %s, %s, %s)
            """
            execute_insert(query, (page_id, header.key, header.label, header.isVisibleInList, header.isVisibleInSingleView))
        
        commit_transaction(cnx)
    except Exception as e:
        rollback_transaction(cnx)
        raise e

def delete_page(page_id: int):
    cnx = start_transaction()
    try:
        query = "DELETE FROM auto_page_builder WHERE id = %s"
        execute_query(query, (page_id,))

        query = "DELETE FROM auto_page_builder_fields WHERE auto_page_builder_id = %s"
        execute_query(query, (page_id,))

        query = "DELETE FROM auto_page_builder_action_labels WHERE auto_page_builder_id = %s"
        execute_query(query, (page_id,))

        query = "DELETE FROM auto_page_builder_headers WHERE auto_page_builder_id = %s"
        execute_query(query, (page_id,))
        
        commit_transaction(cnx)
    except Exception as e:
        rollback_transaction(cnx)
        raise e

def get_pages() -> List[dict]:
    query = """
        SELECT apb.id, apb.modelName, apb.modelUri, apb.apiEndpoint,
               GROUP_CONCAT(DISTINCT CONCAT_WS(':', apbf.name, apbf.type, apbf.label, apbf.isRequired, apbf.dataType, apbf.defaultValue) SEPARATOR ';') AS fields,
               GROUP_CONCAT(DISTINCT CONCAT_WS(':', apbal.key, apbal.label, apbal.actionType, apbal.show) SEPARATOR ';') AS actionLabels,
               GROUP_CONCAT(DISTINCT CONCAT_WS(':', apbh.key, apbh.label, apbh.isVisibleInList, apbh.isVisibleInSingleView) SEPARATOR ';') AS headers
        FROM auto_page_builder apb
        LEFT JOIN auto_page_builder_fields apbf ON apb.id = apbf.auto_page_builder_id
        LEFT JOIN auto_page_builder_action_labels apbal ON apb.id = apbal.auto_page_builder_id
        LEFT JOIN auto_page_builder_headers apbh ON apb.id = apbh.auto_page_builder_id
        GROUP BY apb.id
    """
    results = execute_query(query)
    return results
