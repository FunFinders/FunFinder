import { View, Text } from 'react-native'
import { Tabs } from 'expo-router'
import { Ionicons } from '@expo/vector-icons'

const TabsLayout = () => {
  return (
    <Tabs screenOptions={{
        tabBarActiveTintColor: '#7c5cdb',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle:{
            backgroundColor:"white",
            borderTopWidth: 1,
            borderTopColor: "lightgray",
            height: 90,
            paddingTop: 10
        },
        tabBarLabelStyle:{
            fontSize: 14,
            fontWeight: "600"
        },
        headerShown: false

    }}>

    <Tabs.Screen
        name="index"
        options={{
            title: "Explore",
            tabBarIcon:({color,size})=>(<Ionicons name='search' size={size} color={color}/>)
        }}
    />

    <Tabs.Screen
        name="saved"
        options={{
            title: "Saved",
            tabBarIcon:({color,size})=>(<Ionicons name='bookmark-outline' size={size} color={color}/>)
        }}
    />

    <Tabs.Screen
        name="profile"
        options={{
            title: "Profile",
            tabBarIcon:({color,size})=>(<Ionicons name='person' size={size} color={color}/>)
        }}
    />
    

    </Tabs>
  )
}

export default TabsLayout