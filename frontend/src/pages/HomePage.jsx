import { Container, Title, Text, Button, Card, TextInput } from "@mantine/core";
import { useState } from "react";
import ConnectionTest from "../components/ConnectionTest.jsx";

export default function HomePage() {
  const [name, setName] = useState("");

  return (
    <Container size="sm" mt="xl">
      {/* Title */}
      <Title order={1} mb="md">
        Welcome to Your App
      </Title>

      {/* Text */}
      <Text mb="lg" c="dimmed">
        This is a simple page built with Mantine components.
      </Text>

      {/* Card */}
      <Card shadow="sm" padding="lg" radius="md" withBorder mb="lg">
        <Text fw={500} mb="sm">
          Enter your name:
        </Text>

        {/* TextInput */}
        <TextInput
          placeholder="Your name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          mb="md"
        />

        {/* Button */}
        <Button fullWidth onClick={() => alert(`Hello, ${name || "stranger"}!`)}>
          Greet Me
        </Button>
      </Card>

      <ConnectionTest />

    </Container>
  );
}