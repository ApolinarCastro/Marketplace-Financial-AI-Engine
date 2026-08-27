with open('engine/v4/ingestion/orchestrator.py', 'r', encoding='utf-8') as f:
    text = f.read()

import_log = 'import logging\nlogger = logging.getLogger(__name__)\n\n'
if 'import logging' not in text:
    text = import_log + text

old_except = '''            except Exception as e:
                self.registry.add_error(record, f"{stage_name} exception: {e}")
                break'''
new_except = '''            except Exception as e:
                logger.error(f"Exception in stage {stage_name} for file {record.file_name} (exec: {record.execution_id})", exc_info=True)
                self.registry.add_error(record, f"{stage_name} exception: {e}")
                break'''
text = text.replace(old_except, new_except)

with open('engine/v4/ingestion/orchestrator.py', 'w', encoding='utf-8') as f:
    f.write(text)
