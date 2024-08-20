import { Container, TextField, Button, Typography, FormControl, InputLabel, Select, MenuItem, Grid } from '@mui/material';
import { useState } from 'react';

function App() {
  const [country, setCountry] = useState("");
  const [response, setResponse] = useState("");
  const [continent, setContinent] = useState("");
  const [city, setCity] = useState("");
  const [graph1, setGraph1] = useState("");
  const [graph2, setGraph2] = useState("");
  const [graph3, setGraph3] = useState("");
  const [graph4, setGraph4] = useState("");
  const [graph5, setGraph5] = useState("");
  const [graph6, setGraph6] = useState("");
  const [graph7, setGraph7] = useState("");

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
        // stringify converts the JavaScript object { country } into a JSON string. In this object, country is the key, and its value is whatever the user typed in the text field.
        body: JSON.stringify({ country }),
      });

      console.log("Response received:", res);

      // parses the JSON response from the server into a JS object
      const data = await res.json();
      console.log("Data parsed:", data);
      //  updates the response state with the city_list result from the server or a default message if no response is provided.
      setResponse(data.cities || "No response");
      setContinent(data.continent)
    } catch (error) {
      setResponse("Error: Could not connect to server.");
    }
  };

  const handleCityChoice = e => {
    const selectedCity = e.target.value
    setCity(selectedCity)
    console.log("city chosen: ", selectedCity)
    handleSelect(selectedCity)
  }
  const handleSelect = async (selectedCity) => {
    try {
      const res = await fetch('http://localhost:5000/get-user-city', {
        method: 'POST',
        //informs the server about the format of data being sent
        headers: {
          'Content-Type': 'application/json',
        },
        // actual data being sent to server
        // converts JSON object into a JSON string format
        // stringify converts the JavaScript object { country } into a JSON string. In this object, country is the key, and its value is whatever the user typed in the text field.
        body: JSON.stringify({ country, continent, city: selectedCity }),
      });
      console.log("Second response received:", res);

      // parses the JSON response from the server into a JS object
      const data = await res.json();
      console.log("Hostel data parsed:", data);
      setGraph1('/static/images/graph1.png');
      setGraph2('/static/images/graph2.png');
      setGraph3('/static/images/graph3.png');
      setGraph4('/static/images/graph4.png');
      setGraph5('/static/images/graph5.png');
      setGraph6('/static/images/graph6.png');
      setGraph7('/static/images/graph7.png');
    } catch (error) {
      console.log(error)
    }
  }

  return (
    <Container>
      <Typography>Hostel Search</Typography>
      <Grid>
        <form onSubmit={handleSubmit}>
          <Grid>
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
          </Grid>
          {response && (
          <Grid
            marginTop={5}
          >
          <FormControl sx={{width: 180}}>
            <InputLabel
              sx={{
                '&.MuiInputLabel-shrink':{
                  color:"black"
                },
                fontSize: 25
              }}
            >Choose City</InputLabel>
            <Select
              label="Choose City"
              value={city}
              onChange={e=>handleCityChoice(e)}
            >
              {response.map((choice, i)=>{
                return <MenuItem key={i} value={choice}>{choice}</MenuItem>
              })}
            </Select>
          </FormControl>
          {graph1 && <img src={graph1} alt="hostel-graph"/>}
          {graph2 && <img src={graph2} alt="hostel-graph"/>}
          {graph3 && <img src={graph3} alt="hostel-graph"/>}
          {graph4 && <img src={graph4} alt="hostel-graph"/>}
          {graph5 && <img src={graph5} alt="hostel-graph"/>}
          {graph6 && <img src={graph6} alt="hostel-graph"/>}
          {graph7 && <img src={graph7} alt="hostel-graph"/>}
          </Grid>
          )}
        </form>
      </Grid>
    </Container>
  );
}

export default App;