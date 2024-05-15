'use client'
import React, { useState } from "react";
import { Input, Button } from "@nextui-org/react";
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

export default function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [jwtToken, setJwtToken] = useState("");

  const handleEmailChange = (e: any) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e: any) => {
    setPassword(e.target.value);
  };

  const handleSubmit = () => {
    const uuid = uuidv4();

    const requestData = {
        email: email,
        password: password,
        uuid: uuid
    }

    axios.post('http://localhost:5000/api/createuser', requestData)
      .then(response => {
        const jwtToken = response.data.jwt_token;
        setJwtToken(jwtToken);
        localStorage.setItem('jwtToken', jwtToken);
        window.location.href = "/";
      })
      .catch(error => {
        console.error("Error:", error);
      });
  };

  const handleLogout = () => {
    setJwtToken("");
    localStorage.removeItem('jwtToken');
  };

  return (
    <div className="flex justify-center items-center h-screen overflow-hidden">
      <div className="w-full max-w-[300px] flex flex-col gap-4">
        <Input
          type="email"
          value={email}
          onChange={handleEmailChange}
          label="Email"
          placeholder="Enter your email"
        />
        <Input
          type="password"
          value={password}
          onChange={handlePasswordChange}
          label="Password"
          placeholder="Enter your password"
        />
        <Button
          color="primary"
          variant="ghost"
          className="mt-4 self-end"
          onClick={handleSubmit}
        >
          Create Account
        </Button>
        {jwtToken && (
          <Button
            color="error"
            variant="ghost"
            className="mt-4 self-end"
            onClick={handleLogout}
          >
            Logout
          </Button>
        )}
      </div>
    </div>
  );
}
