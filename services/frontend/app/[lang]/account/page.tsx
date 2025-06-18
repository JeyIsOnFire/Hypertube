"use client"

import styles from "@/app/[lang]/auth/auth.module.css";
import React, {useEffect, useState} from "react";
import {postData} from "@/lib/fetch-api";
import toast from "react-hot-toast";

type User = {
  username?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  preferred_language?: string;
  avatarUrl?: string | null;
}

export default function accountPage() {

    const [userInfos, setUser] = useState<User>({});

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
              console.log('Account update failed:', errorData);
              return;
            }

            const result = await response.json();
            const user: User = {
              username: result.username,
              email: result.email,
              first_name: result.first_name,
              last_name: result.last_name,
              preferred_language: result.preferred_language,
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

      function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
        const { name, value } = e.target;
        setUser((prev) => ({
          ...prev,
          [name]: value,
        }));
      }

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const isValid: boolean = await postData('/users/update/', JSON.stringify(userInfos));
        if (isValid) toast.success("Account updated")
        else toast.error("Error account update");
      };

    return (
        <form id={styles.mainForm} onSubmit={handleSubmit}>
            <h1 id={styles.mainTitle}>Your account</h1>
            <input className="inputStyle1" name="username" type="text" placeholder="Username" value={userInfos.username ?? ''} onChange={handleChange}/>
            <input className="inputStyle1" name="email" type="email" placeholder="Email" value={userInfos.email ?? ''} onChange={handleChange}/>
            <input className="inputStyle1" name="first_name" type="text" placeholder="First Name" value={userInfos.first_name ?? ''} onChange={handleChange}/>
            <input className="inputStyle1" name="last_name" type="text" placeholder="Last Name" value={userInfos.last_name ?? ''} onChange={handleChange}/>
            <input className="inputStyle1" name="password" type="password" placeholder="Change your password" onChange={handleChange}/>
            <input className="inputStyle1" name="confirmPassword" type="password" placeholder="Password confirmation" onChange={handleChange}/>
            <fieldset>
                <legend>Preferred language</legend>

                <div style={{display: 'flex', gap: '15px'}}>
                    <label className="custom-radio">
                        <input type="radio" name="preferred_language" value="en" checked={userInfos.preferred_language === 'en'} onChange={handleChange}/>
                        <span className="radio-mark"></span>
                        English
                    </label>

                    <label className="custom-radio">
                        <input type="radio" name="preferred_language" value="fr" checked={userInfos.preferred_language === 'fr'} onChange={handleChange}/>
                        <span className="radio-mark"></span>
                        French
                    </label>
                </div>
            </fieldset>
            <span>
              <div>Profile picture</div>
              <input className="uploadInputFile" type="file" name="profilePicture" accept="image/*" onChange={handleChange}/>
          </span>
            <button style={{background: 'green', padding: '10px', borderRadius: '5px'}} type="submit">Update profile</button>
        </form>
    )
}