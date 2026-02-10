import { View, Text, StyleSheet, Image, TouchableOpacity, ScrollView } from 'react-native'
import React, { useState } from 'react'
import { Ionicons } from '@expo/vector-icons'

const profile = () => {
  // state to track selected preferences
  const [selectedPreferences, setSelectedPreferences] = useState<string[]>([])

  // toggle pref selection
  const togglePreference = (preference: string) => {
    if (selectedPreferences.includes(preference)) {
      // remove if selected
      setSelectedPreferences(selectedPreferences.filter(p => p !== preference))
    } else {
      // add
      setSelectedPreferences([...selectedPreferences, preference])
    }
  }

  // helper func to check if pref selected
  const isSelected = (preference: string) => {
    return selectedPreferences.includes(preference)
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.profileSection}>
        <View style={styles.avatarContainer}>
          <Image 
            source={{ uri: 'https://m.media-amazon.com/images/M/MV5BNjY3OTQwMDctY2M2Ni00OGE2LThiNjMtYjg0MDg3YjVjN2FiXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg' }} 
            style={styles.avatar}
          />
        </View>
        <Text style={styles.name}>Jack Black</Text>
      </View>

      <View style={styles.preferencesSection}>
        <Text style={styles.preferencesTitle}>Preferences</Text>

        {/* pref buttons, copy paste for more, might make it so it only shows valid types? */}
        <View style={styles.preferencesContainer}>
          <TouchableOpacity 
            style={[
              styles.preferenceButton,
              isSelected('Restaurants') && styles.preferenceButtonSelected
            ]}
            onPress={() => togglePreference('Restaurants')}
          >
            <Text style={[
              styles.preferenceText,
              isSelected('Restaurants') && styles.preferenceTextSelected
            ]}>
              Restaurants
            </Text>
          </TouchableOpacity>

          <TouchableOpacity 
            style={[
              styles.preferenceButton,
              isSelected('Sports') && styles.preferenceButtonSelected
            ]}
            onPress={() => togglePreference('Sports')}
          >
            <Text style={[
              styles.preferenceText,
              isSelected('Sports') && styles.preferenceTextSelected
            ]}>
              Sports
            </Text>
          </TouchableOpacity>

          <TouchableOpacity 
            style={[
              styles.preferenceButton,
              isSelected('Recreation') && styles.preferenceButtonSelected
            ]}
            onPress={() => togglePreference('Recreation')}
          >
            <Text style={[
              styles.preferenceText,
              isSelected('Recreation') && styles.preferenceTextSelected
            ]}>
              Recreation
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  profileSection: {
    alignItems: 'center',
    paddingTop: 60,
    paddingBottom: 30,
    backgroundColor: 'white',
  },
  avatarContainer: {
    position: 'relative',
    marginBottom: 15,
  },
  avatar: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#e0e0e0',
  },
  name: {
    fontSize: 24,
    fontWeight: '600',
    color: '#333',
  },
  preferencesSection: {
    padding: 20,
    marginTop: 20,
  },
  preferencesTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 20,
    textAlign: 'center',
  },
  preferencesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: 15,
  },
  preferenceButton: {
    paddingVertical: 15,
    paddingHorizontal: 30,
    borderRadius: 25,
    backgroundColor: '#e8e4f3',
    minWidth: 140,
    alignItems: 'center',
  },
  preferenceButtonSelected: {
    backgroundColor: '#7c5cdb',
  },
  preferenceText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#7c5cdb',
  },
  preferenceTextSelected: {
    color: 'white',
  },
})

export default profile