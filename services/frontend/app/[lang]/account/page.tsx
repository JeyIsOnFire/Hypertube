"use client"

import styles from "@/app/[lang]/auth/auth.module.css";
import React, {useEffect, useState} from "react";

type User = {
    username: string;
    email: string;
    firstname: string;
    lastname: string;
    language: string;
    avatarUrl: string | null;
}

export default function accountPage() {

    const [userInfos, setUser] = useState<User>();


      useEffect(() => {
        const fetchUser = async () => {
          try {
            const response = await fetch('/users/profile/', {
              method: 'GET',
              headers: {
                "Content-Type": "application/json",
              },
              credentials: "include"
            });

            if (!response.ok) {
              const errorData = await response.json();
              console.log('Login failed:', errorData);
              return;
            }

            const result = await response.json();
            const user: User = {
              username: result.username,
              email: result.email,
              firstname: result.first_name,
              lastname: result.last_name,
              language: result.preferred_language,
              avatarUrl: result.profile_picture,
            };
            setUser(user);
            console.log(userInfos);
          } catch (err) {
            console.error(err);
          }
        };

        fetchUser();
      }, []);

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        try {
          const response = await fetch('/users/login/', {
            method: 'POST',
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({}),
            credentials: "include"
          });

          if (!response.ok) {
            const errorData = await response.json();
            console.log('Login failed:', errorData);
            return;
          }

          const result = await response.json();
          console.log(result)
        } catch (err) {
          console.log('Login failed:', err);
        }
      };

    return (
        <form id={styles.mainForm} onSubmit={handleSubmit}>
            <h1 id={styles.mainTitle}>Profile</h1>
            <input className="inputStyle1" name="username" type="text" placeholder="Username"/>
            <input className="inputStyle1" name="password" type="password" placeholder="Password"
                   />
            <input className="inputStyle1" name="confirmPassword" type="password" placeholder="Password confirmation"
                   />
            <input className="inputStyle1" name="email" type="email" placeholder="Email" />
            <input className="inputStyle1" name="first_name" type="text" placeholder="First Name"
                   />
            <input className="inputStyle1" name="last_name" type="text" placeholder="Last Name"
                   />
            <fieldset>
                <legend>Preferred language</legend>

                <div style={{display: 'flex', gap: '15px'}}>
                    <label className="custom-radio">
                        <input type="radio" name="preferredLanguage" value="eng" defaultChecked
                               />
                        <span className="radio-mark"></span>
                        English
                    </label>

                    <label className="custom-radio">
                        <input type="radio" name="preferredLanguage" value="fr" />
                        <span className="radio-mark"></span>
                        French
                    </label>
                </div>
            </fieldset>
            <span>
              <div>Profile picture</div>
              <input className="uploadInputFile" type="file" name="profilePicture" accept="image/*"
                     />
          </span>
            <button style={{background: 'green', padding: '10px', borderRadius: '5px'}} type="submit">Update profile</button>
        </form>
    )
}