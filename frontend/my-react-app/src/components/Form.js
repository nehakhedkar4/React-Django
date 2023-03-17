import React, { useState } from 'react';
import axios from 'axios';

const Form = () => {
    // Use state to store the form data
  const [formData, setFormData] = useState({
    name: '',
    fname: ''
  });

  // Handle form submit
  const handleSubmit = async e => {
    e.preventDefault();
    try {
      // Use Axios to send a POST request to the API endpoint
      const response = await axios.post('http://127.0.0.1:8000/test2/', formData);

      // Handle the response data
      console.log(response.data);
    } catch (error) {
      // Handle any errors
      console.error(error);
    }
  };

  // Handle form input change
  const handleChange = e => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };
  return (
    <form onSubmit={handleSubmit}>
    <label>
      Name:
      <input type="text" name="name" onChange={handleChange} />
    </label>
    <br />
    <label>
      fname:
      <input type="text" name="fname" onChange={handleChange} />
    </label>
    <br />
    <button type="submit">Submit</button>
  </form>
  )
}

export default Form