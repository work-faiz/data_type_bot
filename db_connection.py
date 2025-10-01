import sqlite3
from datetime import datetime
import configparser
import os

# Read database configuration
config = configparser.ConfigParser()
config.read('config.properties')

def get_db_connection():
    """Get database connection based on configuration"""
    db_type = config.get('database', 'db_type', fallback='sqlite')
    
    if db_type.lower() == 'mysql':
        try:
            import mysql.connector
            conn = mysql.connector.connect(
                host=config.get('database', 'host'),
                user=config.get('database', 'user'),
                password=config.get('database', 'password'),
                port=int(config.get('database', 'port', fallback=3306)),
                database=config.get('database', 'database_name')
            )
            return conn
        except ImportError:
            print("MySQL connector not installed. Install with: pip install mysql-connector-python")
            return None
        except Exception as e:
            print(f"Error connecting to MySQL: {str(e)}")
            return None
            
    elif db_type.lower() == 'postgresql':
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=config.get('database', 'host'),
                user=config.get('database', 'user'),
                password=config.get('database', 'password'),
                port=int(config.get('database', 'port', fallback=5432)),
                database=config.get('database', 'database_name')
            )
            return conn
        except ImportError:
            print("PostgreSQL connector not installed. Install with: pip install psycopg2-binary")
            return None
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {str(e)}")
            return None
            
    else:  # Default to SQLite
        db_path = config.get('database', 'db_path', fallback='ai_data.db')
        conn = sqlite3.connect(db_path)
        # Enable dict-like row access for SQLite
        conn.row_factory = sqlite3.Row
        return conn


def can_we_start(config):
    try:
        conn = get_db_connection()
        if conn is None:
            print("Failed to establish database connection")
            return False
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {config.get("TABLE", "name")} WHERE bot_status isnull;')
        rows = cursor.fetchall()
        if len(rows) >= 1:
            return True
        return False
    except Exception as e:
        raise Exception(f"Error checking if we can start: {str(e)}") from e

def save_data(db_id):
    try:
        conn = get_db_connection()
        if conn is None:
            print("Failed to establish database connection")
            return False
        cursor = conn.cursor()
        query = f"""update {config.get("TABLE", "name")} set bot_status = 'Completed', bot_completion_time=now() where id = {db_id};"""
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as err:
        raise Exception(f"Error at save data: {str(err)}") from err


def save_data_error(db_id, error):
    try:
        conn = get_db_connection()
        if conn is None:
            print("Failed to establish database connection")
            return False
        cursor = conn.cursor()
        query = f"""update {config.get("TABLE", "name")} set bot_status = 'Failed', bot_completion_time=now(), bot_error='{error.replace("'","")}' 
                    where id = {db_id};"""
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as err:
        raise Exception(f"Error at save data error: {str(err)}") from err


def get_data(config):
    """View all saved AI data from the database"""
    try:
        conn = get_db_connection()
        if conn is None:
            print("Failed to establish database connection")
            return []
            
        db_type = config.get('database', 'db_type', fallback='sqlite').lower()

        # Create a cursor that yields dictionaries when possible
        if db_type == 'mysql':
            cursor = conn.cursor(dictionary=True)
        elif db_type == 'postgresql':
            cursor = conn.cursor()
        else:
            cursor = conn.cursor()
        
        cursor.execute(f'SELECT * FROM {config.get("TABLE", "name")} WHERE bot_status isnull ORDER BY id limit 1;')
        rows = cursor.fetchall()
        
        if not rows:
            print("No data found in database")
            conn.close()
            return {}

        result_dict = {}
        header = [desc[0] for desc in cursor.description]
        for key, value in zip(header, rows[0]):
            result_dict[key] = value
        
        query = f"""update {config.get("TABLE", "name")} set bot_status = 'WIP', bot_pickup_time=now() where id = {result_dict['id']};"""
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        return result_dict
    except Exception as e:
        print(f"Error viewing database: {str(e)}")
        if 'conn' in locals() and conn:
            conn.close()

def export_data_to_csv():
    """Export all AI data from database to CSV file"""
    try:
        import csv
        conn = get_db_connection()
        if conn is None:
            print("Failed to establish database connection")
            return None
            
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM ai_data ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        if not rows:
            print("No data found in database to export")
            return None
        
        csv_filename = f'ai_data_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow([
                'ID', 'URL', 'Website Status', 'Address', 'City', 'State', 
                'Company Profile', 'Product Name', 'Product Description', 
                'Product Image', 'Business Type', 'Email', 'Phone', 'Country', 'Timestamp'
            ])
            
            # Write data
            for row in rows:
                writer.writerow(row)
        
        conn.close()
        print(f"Data exported to {csv_filename}")
        return csv_filename
    except Exception as e:
        print(f"Error exporting to CSV: {str(e)}")
        if 'conn' in locals() and conn:
            conn.close()
        return None
