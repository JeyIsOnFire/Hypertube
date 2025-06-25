"use client";

import React from 'react';
import styles from '../auth.module.css'
import { useState } from "react";
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {postData} from "@/lib/fetch-api";
import toast from "react-hot-toast";
import {isDataFilled} from "@/lib/utils";
import OAuth from "@/app/[lang]/auth/oauth/page";

export default function loginPage() {

  const router = useRouter();
  const initialFormData = {
    username: "",
    password: "",
  };

  const [formData, setFormData] = useState(initialFormData);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const isValid: boolean = await postData("/users/login/", JSON.stringify(formData))
    if (isValid) {
      toast.success("Logged in")
      router.push('/');
    } else toast.error("Error login");
    setFormData(initialFormData);
  };

  function OAuthLogin(event: React.FormEvent<HTMLFormElement>) {
    const id = "u-s4t2ud-2c90b78954c87807b2c6a5381a3d1923e0737de30580e8b2a27f0ee0cdb97460";
    const red = "https://localhost:8443/users/oauth_42/"
    const url = `https://api.intra.42.fr/oauth/authorize?client_id=${id}&redirect_uri=${red}&response_type=code`
    window.location.href = url;
  }

  return (
      <div>
        <form id={styles.mainForm} onSubmit={handleSubmit}>
          <h1 id={styles.mainTitle}>Login</h1>
          <input className="inputStyle1" name="username" type="text" placeholder="Username" value={formData.username} onChange={handleChange}/>
          <input className="inputStyle1" name="password" type="password" placeholder="Password" value={formData.password} onChange={handleChange}/>

          <button className={styles.button} type="submit" disabled={!isDataFilled(Object.values(formData))}>Login</button>

          <OAuth></OAuth>

          <Link href="/auth/register">You don't have an account ?</Link>
        </form>
      </div>
  );
}