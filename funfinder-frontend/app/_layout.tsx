import { Stack } from "expo-router";

export default function RootLayout() {
  // A stack of screens
  return <Stack screenOptions={{ headerShown: false }}>
    <Stack.Screen name="(tabs)}" />
  </Stack>;
}
