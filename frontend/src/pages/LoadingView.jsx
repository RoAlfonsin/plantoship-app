import { Container, Center, Loader, Text, Card, Stack } from "@mantine/core";

export default function LoadingPage() {
  return (
    <Container size="xs" h="100vh">
      <Center h="100%">
        <Card shadow="sm" padding="xl" radius="md" withBorder>
          <Stack align="center" gap="md">
            {/* Loader */}
            <Loader size="lg" variant="dots" />

            {/* Text */}
            <Text size="lg" fw={500}>
              Loading...
            </Text>

            <Text size="sm" c="dimmed">
              Please wait while we prepare everything for you.
            </Text>
          </Stack>
        </Card>
      </Center>
    </Container>
  );
}