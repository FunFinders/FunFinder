import { View, Text, StyleSheet, TouchableOpacity } from 'react-native'
import React, { useState } from 'react'

const API_URL = 'http://11.20.8.58:5000';

interface PlaceCardProps {
    id: string;
    name: string;
    rating: number;
    priceLevel: number;
    onPress: () => void;
}


const PlaceCard = ({ id, name, rating, priceLevel, onPress }: PlaceCardProps) => {
    const [saved, setSaved] = useState(false);
    const [liked, setLiked] = useState(false);
    const [visited, setVisited] = useState(false);

    const renderPriceLevel = (level: number) => {
        if (!level) return 'N/A';
        return '$'.repeat(level);
    }
    const handleSave = () => {
        fetch(`${API_URL}/${saved ? 'unsave' : 'save'}/${id}`, { method: 'POST' });
        setSaved(!saved);
    }; 

    const handleLike = () => {
        fetch(`${API_URL}/${liked ? 'unlike' : 'like'}/${id}`, { method: 'POST' });
        setLiked(!liked);
    };

    const handleVisit = () => {
        fetch(`${API_URL}/${visited ? 'unvisit' : 'visit'}/${id}`, { method: 'POST' });
        setVisited(!visited);  // visits are one-way (it's a history), can't undo from here
    };

    return (
        <TouchableOpacity style={styles.card} onPress={onPress}>
            <Text style={styles.name}>{name}</Text>
 
            <View style={styles.info}>
                <Text style={styles.label}>Rating: {rating ? rating.toFixed(1) : 'N/A'}</Text>
                <Text style={styles.label}>Price: {renderPriceLevel(priceLevel)}</Text>
            </View>
 
            <View style={styles.actions}>
                <TouchableOpacity style={[styles.btn, saved && styles.btnActive]} onPress={handleSave}>
                    <Text style={styles.btnText}>{saved ? 'Saved' : 'Save'}</Text>
                </TouchableOpacity>
 
                <TouchableOpacity style={[styles.btn, liked && styles.btnActive]} onPress={handleLike}>
                    <Text style={styles.btnText}>{liked ? 'Liked' : 'Like'}</Text>
                </TouchableOpacity>
 
                <TouchableOpacity style={[styles.btn, visited && styles.btnActive]} onPress={handleVisit}>
                    <Text style={styles.btnText}>{visited ? 'Visited' : 'Visit'}</Text>
                </TouchableOpacity>
            </View>
        </TouchableOpacity>
    );
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
  actions: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 8,
  },
  btn: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
    backgroundColor: '#e8e4f3',
  },
  btnActive: {
    backgroundColor: '#7c5cdb',
  },
  btnText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#333',
  },
})

export default PlaceCard