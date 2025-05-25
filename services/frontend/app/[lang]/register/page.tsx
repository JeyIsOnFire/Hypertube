"use client";

import React from 'react';
import styles from './register.module.css'

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
      <form id={styles.registerForm} onSubmit={handleSubmit}>
        <h1 style={{fontSize: '3em'}}>Register</h1>
        <input className="inputStyle1" type="text" placeholder="Username"/>
        <input className="inputStyle1" type="password" placeholder="Password"/>
        <input className="inputStyle1" type="password" placeholder="Password confirmation"/>
        <input className="inputStyle1" type="email" placeholder="Email"/>
        <input className="inputStyle1" type="text" placeholder="First Name"/>
        <input className="inputStyle1" type="text" placeholder="Last Name"/>
        <fieldset>
          <legend>Preferred language</legend>

          <div style={{display: 'flex'}}>
            <label className="custom-radio">
              <input type="radio" name="lang" value="eng" defaultChecked />
              <span className="radio-mark"></span>
              English
            </label>

            <label className="custom-radio">
              <input type="radio" name="lang" value="fr"/>
              <span className="radio-mark"></span>
              French
            </label>
          </div>
        </fieldset>
        <span>
            <div>Profile picture (Optional)</div>
            <input className="uploadInputFile" type="file" id="images" accept="image/*"/>
        </span>
        <button style={{background: 'green', padding: '10px', borderRadius: '5px'}} type="submit">Register</button>
        <a>Already register ?</a>
      </form>
    </div>
  );
}

export default registerPage;
