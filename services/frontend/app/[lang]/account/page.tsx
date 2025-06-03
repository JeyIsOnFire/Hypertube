"use client"

import styles from "@/app/[lang]/auth/auth.module.css";
import React from "react";

export default function accountPage() {
    return (
        <form id={styles.mainForm} onSubmit={handleSubmit}>
            <h1 id={styles.mainTitle}>Profile</h1>
            <input className="inputStyle1" name="username" type="text" placeholder="Username" onChange={handleChange}/>
            <input className="inputStyle1" name="password" type="password" placeholder="Password"
                   onChange={handleChange}/>
            <input className="inputStyle1" name="confirmPassword" type="password" placeholder="Password confirmation"
                   onChange={handleChange}/>
            <input className="inputStyle1" name="email" type="email" placeholder="Email" onChange={handleChange}/>
            <input className="inputStyle1" name="first_name" type="text" placeholder="First Name"
                   onChange={handleChange}/>
            <input className="inputStyle1" name="last_name" type="text" placeholder="Last Name"
                   onChange={handleChange}/>
            <fieldset>
                <legend>Preferred language</legend>

                <div style={{display: 'flex', gap: '15px'}}>
                    <label className="custom-radio">
                        <input type="radio" name="preferredLanguage" value="eng" defaultChecked
                               onChange={handleChange}/>
                        <span className="radio-mark"></span>
                        English
                    </label>

                    <label className="custom-radio">
                        <input type="radio" name="preferredLanguage" value="fr" onChange={handleChange}/>
                        <span className="radio-mark"></span>
                        French
                    </label>
                </div>
            </fieldset>
            <span>
              <div>Profile picture</div>
              <input className="uploadInputFile" type="file" name="profilePicture" accept="image/*"
                     onChange={handleChange}/>
          </span>
            <button style={{background: 'green', padding: '10px', borderRadius: '5px'}} type="submit">Update profile</button>
        </form>
    )
}