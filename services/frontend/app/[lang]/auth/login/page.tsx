"use client";

import React from 'react';
import styles from '../auth.module.css'
import { useState } from "react";
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {postData} from "@/lib/fetch-api";
import toast from "react-hot-toast";
import {isDataFilled} from "@/lib/utils";

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

  return (
    <form id={styles.mainForm} onSubmit={handleSubmit}>
      <h1 id={styles.mainTitle}>Login</h1>
      <input className="inputStyle1" name="username" type="text" placeholder="Username" value={formData.username} onChange={handleChange}/>
      <input className="inputStyle1" name="password" type="password" placeholder="Password" value={formData.password} onChange={handleChange}/>

      <button className={styles.button} type="submit" disabled={!isDataFilled(Object.values(formData))}>Login</button>
      <Link href="/auth/register">You don't have an account ?</Link>
    </form>
  );
}