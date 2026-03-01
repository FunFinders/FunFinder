import { View, Text, StyleSheet, TouchableOpacity } from 'react-native'
import React from 'react'

interface PlaceCardProps {
    id: string;
    name: string;
    rating: number;
    priceLevel: number;
    onPress: () => void;
}


const PlaceCard = ({ id, name, rating, priceLevel, onPress }: PlaceCardProps) => {
    const renderPriceLevel = (level: number) => {
        if (!level) return 'N/A';
        return '$'.repeat(level);
    }

    return (
    <TouchableOpacity style={styles.card} onPress={onPress}>
      <Text style={styles.name}>{name}</Text>
      
      <View style={styles.info}>
        <Text style={styles.label}>Rating: {rating ? rating.toFixed(1) : 'N/A'}</Text>
        <Text style={styles.label}>Price: {renderPriceLevel(priceLevel)}</Text>
      </View>
    </TouchableOpacity>
  )
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: 'white',
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 67,
    marginHorizontal: 16,
    marginVertical: 10,
  },
  name: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  info: {
    flexDirection: 'row',
    gap: 20,
  },
  label: {
    fontSize: 14,
    color: '#666',
  },
})

export default PlaceCard