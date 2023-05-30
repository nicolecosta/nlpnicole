from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import HTMLResponse 
from classifier import classify_prompt, label_encoder
import uvicorn
import os

app = FastAPI()

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Mount the static files directory
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# Define request model
class ClassificationRequest(BaseModel):
    prompt: str

# Define response model
class ClassificationResponse(BaseModel):
    prediction: str

@app.post("/classify")
async def classify(request: ClassificationRequest):
    # Extract the prompt from the request
    prompt = request.prompt

    # Perform classification using your classifier function
    prediction = classify_prompt(prompt)

    # Decode the encoded prediction using the LabelEncoder
    decoded_prediction = label_encoder.inverse_transform([prediction])[0]

    # Create the response
    response = ClassificationResponse(prediction=decoded_prediction)

    # Extract the prediction value as a string
    classification_result = response.prediction

    # Create a dictionary with the classification result
    result_dict = {"classification": classification_result}

    return result_dict

# Route for the root URL ("/") to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return open(os.path.join(current_dir, "static/index.html")).read()

# Run the FastAPI app using Uvicorn server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
