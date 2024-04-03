import tflite_runtime.interpreter as tflite
import numpy as np
import json


MODEL_PATH = './models/xxxxxxx.tflite'  # TODO: Specify tflite model


def lambda_handler(event, context):
    """lambda handler
    """
    model = TFLiteModel(MODEL_PATH)

    body = json.loads(event['body'])

    # TODO: Prepare input data (ndarray)
    # -------------------------------
    input_list = body['items']
    input_np = np.array(input_list)
    # -------------------------------

    result = model.predict(input_np)

    return {'statusCode': 200,
            'body': result}


class TFLiteModel:
    """TensorFlow Lite Model
    """
    def __init__(self, tflite_model):
        # Load the TFLite model
        self._interpreter = tflite.Interpreter(model_path=tflite_model)

        # Allocate tensors
        self._interpreter.allocate_tensors()

        # Set input and output tensors
        self.input_details = self._interpreter.get_input_details()
        self.output_details = self._interpreter.get_output_details()

        # Set input shape
        self.input_shape = self.input_details[0]['shape']

    def predict(self, input_data):
        """Execute prediction

        Args:
            input_data (ndarray): data to be predicted

        Raises:
            HTTPException: Application Error

        Returns:
            str: result
        """
        # Execute prediction
        output_data = self.__predict(input_data)

        # TODO: Process output_data if necessary
        result = output_data

        return result

    def __predict(self, input_data):
        # Convert dtype from float64 to float32
        input_data = np.array(input_data, dtype='float32')  

        # Set inputs
        self._interpreter.set_tensor(self.input_details[0]['index'], input_data)

        # Execute
        self._interpreter.invoke()

        output_data = self._interpreter.get_tensor(self.output_details[0]['index'])

        return output_data
