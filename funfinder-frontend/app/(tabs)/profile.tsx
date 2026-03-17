import { View, Text, StyleSheet, Image, TouchableOpacity, ScrollView } from 'react-native'
import React, { useState, useEffect } from 'react'
import { Ionicons } from '@expo/vector-icons'
import { Slider } from '@rneui/themed';

const API_URL = 'http://11.20.8.58:5000';

const profile = () => {

  // placeholder perfernces
  const ALL_PREFERENCES = ['acai_shop', 'american_restaurant', 'asian_restaurant', 'athletic_field', 'atm', 'bagel_shop', 'bakery', 'bar', 'bar_and_grill', 'barbecue_restaurant',
     'bowling_alley', 'brazilian_restaurant', 'breakfast_restaurant', 'brunch_restaurant', 'buffet_restaurant', 'cafe', 'cafeteria', 'candy_store', 'catering_service', 'chinese_restaurant',
      'coffee_shop', 'confectionery', 'convenience_store', 'deli', 'dessert_restaurant', 'dessert_shop', 'diner', 'donut_shop', 'establishment', 'event_venue', 'fast_food_restaurant', 'finance', 'fine_dining_restaurant',
       'food', 'food_court', 'food_delivery', 'food_store', 'french_restaurant', 'gas_station', 'golf_course', 'greek_restaurant', 'grocery_store', 'hamburger_restaurant', 'health', 'ice_cream_shop', 'indian_restaurant',
        'internet_cafe', 'italian_restaurant', 'japanese_restaurant', 'juice_shop', 'korean_restaurant', 'liquor_store', 'meal_delivery', 'meal_takeaway', 'mediterranean_restaurant', 'mexican_restaurant', 'middle_eastern_restaurant',
         'night_club', 'pizza_restaurant', 'point_of_interest', 'pub', 'public_bathroom', 'ramen_restaurant', 'restaurant', 'sandwich_shop', 'school', 'seafood_restaurant', 
    'sporting_goods_store', 'sports_activity_location', 'sports_club', 'sports_coaching', 'sports_complex', 'steak_house', 'store', 'sushi_restaurant',
     'swimming_pool', 'tea_house', 'thai_restaurant', 'turkish_restaurant', 'vegan_restaurant', 'vegetarian_restaurant', 'video_arcade', 'vietnamese_restaurant', 'wholesaler', 'wine_bar'];

  // state to track selected preferences
  const [selectedPreferences, setSelectedPreferences] = useState<string[]>([])

  // state to track rating slider
  const [rating, setRating] = useState(3);

  // state to track price slider
  const [price, setPrice] = useState(3);

  useEffect(() => {
      fetch(`${API_URL}/preferred_types`)
          .then(res => res.json())
          .then(data => setSelectedPreferences(data))
          .catch(err => console.error('Error loading preferences:', err));
  }, []);

  // Toggle a preference: POST to add or remove on the backend
  const togglePreference = (pref: string) => {
      if (selectedPreferences.includes(pref)) {
          fetch(`${API_URL}/remove_preference/${pref}`, { method: 'POST' });
          setSelectedPreferences(selectedPreferences.filter(p => p !== pref));
      } else {
          fetch(`${API_URL}/add_preference/${pref}`, { method: 'POST' });
          setSelectedPreferences([...selectedPreferences, pref]);
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

        {/* dynamically render a button for each type */}
        <View style={styles.preferencesContainer}>
            {ALL_PREFERENCES.map(pref => (
                <TouchableOpacity
                    key={pref}
                    style={[styles.preferenceButton, isSelected(pref) && styles.preferenceButtonSelected]}
                    onPress={() => togglePreference(pref)}
                >
                    <Text style={[styles.preferenceText, isSelected(pref) && styles.preferenceTextSelected]}>
                        {pref.replace(/_/g, ' ')}
                    </Text>
                </TouchableOpacity>
            ))}
        </View>

        <View style={styles.ratingSection}>
            <Text style={styles.ratingTitle}>Rating</Text>
            <Slider
                value={rating}
                onValueChange={setRating}
                minimumValue={1} maximumValue={5}
                allowTouchTrack step={1}
                trackStyle={styles.ratingTrack}
                thumbStyle={styles.ratingThumb}
                thumbProps={{ children: <Text style={styles.ratingThumbLabel}>{rating}</Text> }}
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