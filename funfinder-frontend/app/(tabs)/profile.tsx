import { View, Text, StyleSheet, Image, TouchableOpacity, ScrollView } from 'react-native'
import React, { useState } from 'react'
import { Ionicons } from '@expo/vector-icons'
import { Slider } from '@rneui/themed';

const profile = () => {
  // state to track selected preferences
  const [selectedPreferences, setSelectedPreferences] = useState<string[]>([])

  // state to track rating slider
  const [rating, setRating] = useState(3);

  // state to track price slider
  const [price, setPrice] = useState(3);

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

        <View style={styles.ratingSection}>
          <Text style={styles.ratingTitle}>
            Rating
          </Text>
          <Slider
          value={rating}
          onValueChange={setRating}
          minimumValue={1}
          maximumValue={5}
          allowTouchTrack={true}
          step={1}
          trackStyle={styles.ratingTrack}
          thumbStyle={styles.ratingThumb}
          thumbProps={{
          children: (
            <Text style={styles.ratingThumbLabel}>
              {rating}
            </Text>
          ),}}
          />
        </View>

        <View style={styles.ratingSection}>
          <Text style={styles.ratingTitle}>
            Price
          </Text>
          <Slider
          value={price}
          onValueChange={setPrice}
          minimumValue={1}
          maximumValue={5}
          allowTouchTrack={true}
          step={1}
          trackStyle={styles.ratingTrack}
          thumbStyle={styles.ratingThumb}
          thumbProps={{
          children: (
            <Text style={styles.ratingThumbLabel}>
              {price}
            </Text>
          ),}}
          />
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
  ratingSection: {
    padding: 20,
  },
  ratingTitle: {
    fontSize: 20,
    color: '#333',
  },
  ratingTrack: {
    height: 8,
    borderRadius: 999,
  },
  ratingThumb: {
    height: 20,
    width: 20,
    borderRadius: 999,
    backgroundColor: '#7c5cdb', //color of the circle
  },
  ratingThumbLabel: {
    position: "absolute",
    fontWeight: 'bold',
    fontSize: 19,
    top: -25,
    width: 40,
    textAlign: "center",
  },
  ratingSideLabel: {
    width: 40,          // keeps labels aligned
    textAlign: "center",
    fontSize: 12,
  },
})

export default profile