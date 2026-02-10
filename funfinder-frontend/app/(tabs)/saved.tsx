import { View, Text } from 'react-native'
import React from 'react'

// only renders to areas of the screen that are in view, so no need for padding in search bar
import { SafeAreaView } from 'react-native-safe-area-context';

const saved = () => {
  return (
    <SafeAreaView>
      <Text>saved</Text>
    </SafeAreaView>
  )
}

export default saved