"use client";

import React from 'react';

export default function Test() {

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault(); // optional, in case used in a form

    try {
      const response = await fetch('/users/', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ /* your data here */ }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('Registration failed:', errorData);
        return;
      }

      const result = await response.json();
      console.log(result);
    } catch (err) {
      console.error('Request failed:', err);
    }
  };

  return (
    <div>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}