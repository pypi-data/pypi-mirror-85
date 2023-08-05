from firebase_admin import firestore
import threading


class MLTrainingCompletedNotifier:
    def __init__(self, username, user_logs_name):
        self.username = username
        self.callback_done = threading.Event()

        realtime_db = firestore.client()
        cols = realtime_db.collection(u'training_logs')

        user_ref = cols.document(u'' + self.username)

        self.current_log_doc = user_ref.collection(
            "ml_train_logs").document(u'' + user_logs_name)

        self.result = None

    def wait_for_result(self):
        self.doc_watch = self.current_log_doc.on_snapshot(self.on_snapshot)
        self.callback_done.wait(timeout=3600)
        return self.result

    def on_snapshot(self, doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            logs = doc.get('logs')

            latest = logs[-1]

            if latest['meta'] == "":
                return

            print(latest)

            if latest['meta']['state'] == "COMPLETED":
                self.result = latest['meta']
                self.callback_done.set()
