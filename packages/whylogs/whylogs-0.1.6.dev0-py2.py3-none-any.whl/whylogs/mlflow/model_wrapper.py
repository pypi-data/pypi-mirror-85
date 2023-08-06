import whylogs
import boto3
import datetime


class ModelWrapper(object):
    def __init__(self, model):
        self.model = model
        self.session = whylogs.get_or_create_session()
        self.logger = self.session.logger("mlflow")
        self.s3 = boto3.client("s3")
        self.last_upload_time = datetime.datetime.utcnow()

    def predict(self, input):
        now = datetime.datetime.utcnow()
        delta = now - self.last_upload_time
        if delta.total_seconds() > 15:
            tmp_path = "/tmp/protobuf.data"
            self.logger.profile.write_protobuf(tmp_path, delimited_file=True)
            output = f"sagemaker/{now.timestamp()}-profile.bin"
            print(("Uploading to : ", output))
            self.s3.upload_file(tmp_path, "whylabs-andy-data-us-west-2", output)
            self.last_upload_time = now
            self.logger.close()
            print("Creating new whylogs session")
            self.logger = self.session.logger("mlflow")
        self.logger.log_dataframe(input)
        return self.model.predict(input)
