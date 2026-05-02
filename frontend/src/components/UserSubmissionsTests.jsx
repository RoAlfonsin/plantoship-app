import React, { useState } from "react";
import { Container, Button, TextInput, Group, Text } from "@mantine/core";

const UserSubmissionsTests = () => {
  const API_URL = import.meta.env.VITE_API_URL+"/user-submissions";  
  const [idea, setIdea] = useState("");
  const stack = {
    frontend: "React",
    backend: "FastAPI",
    database: "MongoDB",
    deployment: "Railway",
  };
  const handleCheckIdea = async () => {
    try {
      const response = await fetch(`${API_URL}/api/check-idea`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ idea, stack }),
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container>
      <Group gap="md">
        <TextInput
          value={idea}
          onChange={(event) => setIdea(event.currentTarget.value)}
          placeholder="Enter your project idea"
        />
        <Button onClick={handleCheckIdea}>Check Idea</Button>
      </Group>
    </Container>
  );
};

export default UserSubmissionsTests;