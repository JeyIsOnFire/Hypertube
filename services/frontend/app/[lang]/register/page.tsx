"use client";

import React from 'react';

const registerPage = () => {

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    const response = await fetch('/users/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: event.target[0].value,
        password: event.target[1].value,
        email: event.target[2].value,
        first_name: event.target[3].value,
        last_name: event.target[4].value,
        preferredLanguage: event.target[5].value,
        profilePicture: event.target[6].files[0],
      }),
    });
    if (response.ok) {
      const data = await response.json();
      console.log('Registration successful:', data);
    }
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1 style={{marginBottom: '30px'}}>Register</h1>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <input style={{border: '1px solid black', marginBottom: '20px', padding: '5px'}} type="text" placeholder="Username" />
        <input style={{border: '1px solid black', marginBottom: '20px', padding: '5px'}}  type="password" placeholder="Password" />
        <input style={{border: '1px solid black', marginBottom: '20px', padding: '5px'}} type="email" placeholder="Email" />
        <input style={{border: '1px solid black', marginBottom: '20px', padding: '5px'}} type="text" placeholder="First Name" />
        <input style={{border: '1px solid black', marginBottom: '20px', padding: '5px'}} type="text" placeholder="Last Name" />
        <input style={{border: '1px solid black', marginBottom: '20px', padding: '5px'}} type="text" placeholder="Preferred Language" />
        <input
          style={{ border: '1px solid black', marginBottom: '20px' }}
          type="file"
          accept="image/*"
          placeholder="Upload Profile Picture"
        />
        <button style={{background: 'green', padding: '10px', borderRadius: '5px'}} type="submit">Register</button>
      </form>
    </div>
  );
}

export default registerPage;
