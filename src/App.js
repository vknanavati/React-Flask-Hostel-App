import { Container, TextField, Button, Typography } from '@mui/material';
import { useState } from 'react';

function App() {
  const [country, setCountry] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Form submitted with country:", country);

    // send the country name to the Flask backend
    try {
      const res = await fetch('http://localhost:5000/get-country', {
        method: 'POST',
        //informs the server about the format of data being sent
        headers: {
          'Content-Type': 'application/json',
        },
        // actual data being sent to server
        // converts JSON object country into a JSON string format
        // '{"country": "Canada"}' is the result of JSON.stringify
        // This line converts the JavaScript object { country } into a JSON string. In this object, country is the key, and its value is whatever the user typed in the text field.
        body: JSON.stringify({ country }),
      });

      console.log("Response received:", res);

      // parses the JSON response from the server into a JS object
      const data = await res.json();
      console.log("Data parsed:", data);
      //  updates the response state with the message from the server or a default message if no response is provided.
      // const data = { message: "Received country: France"};
      setResponse(data.message || "No response");
    } catch (error) {
      setResponse("Error: Could not connect to server.");
    }
  };

  return (
    <Container>
      <Typography>Hostel Search</Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          type="text"
          placeholder="Enter country"
          value={country}
          onChange={(e) => setCountry(e.target.value)}
        />
        <Button
          type="submit"
        >
          Submit
        </Button>
      </form>

    </Container>
  );
}

export default App;