'use client'
import React, { useState } from "react";
import { Input, Button } from "@nextui-org/react";
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';



export default function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleEmailChange = (e: any) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e: any) => {
    setPassword(e.target.value);
  };

  const handleSubmit = () => {
    const uuid = uuidv4();

    const requestdata = {
        email: email,
        password: password,
        uuid: uuid
    }

    axios.post('http://localhost:3067/api/createuser', requestdata).then(response => {
        const jwtToken = response.data.token
        localStorage.setItem('jwtToken', jwtToken)
    })


    console.log("Email:", email);
    console.log("Password:", password);
  };

  return (
    <div className="flex justify-center items-center h-screen">
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
      </div>
    </div>
  );
}
