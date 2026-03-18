import { View, Text, FlatList, StyleSheet } from 'react-native'
import React, { useCallback, useEffect, useState } from 'react'

// only renders to areas of the screen that are in view, so no need for padding in search bar
import { SafeAreaView } from 'react-native-safe-area-context';
import PlaceCard from '../components/placecards';
import { useFocusEffect } from '@react-navigation/native';

const API_URL = 'http://127.0.0.1:5000';

const saved = () => {
  const [places, setPlaces] = useState<any[]>([]);

  const fetchPlaces = () => {
    fetch(`${API_URL}/saved/`)
      .then(savedRes => savedRes.json())
      .then((savedPlaces: any) => {
        const ids = Array.isArray(savedPlaces)
          ? savedPlaces.filter((id: any) => typeof id === 'string' && id.length > 0)
          : [];

        return Promise.all(
          ids.map((id: string) =>
            fetch(`${API_URL}/place/${encodeURIComponent(id)}`).then(res => res.json())
          )
        );
      })
      .then(detailedPlaces => {
        setPlaces(detailedPlaces);
      })
      .catch(error => {
        console.error('Error fetching places:', error);
      });
  }

  useFocusEffect(useCallback(() => {
    fetchPlaces();
  }, []));

  const renderPlaceCard = ({ item }: any) => (
    <PlaceCard
        id={item.id}
        name={item.name}
        rating={item.rating}
        priceLevel={item.priceLevel}
        onPress={fetchPlaces}
        savedInit={true}
    />
);

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Saved</Text>
      <FlatList
                data={places}
                renderItem={renderPlaceCard}
                keyExtractor={(item) => item.id}
                contentContainerStyle={styles.listContent}
                showsVerticalScrollIndicator={false}
      />
    </SafeAreaView>
  )
}
const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    flex: 1,
    justifyContent: 'center',
    fontSize: 20,
    fontWeight: 'bold',
  },
  listContent: {
      paddingVertical: 6,
  },
});

export default saved