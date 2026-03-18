import { useFocusEffect } from '@react-navigation/native';
import { SearchBar } from '@rneui/themed';
import * as Location from 'expo-location';
import { SetStateAction, useCallback, useEffect, useState } from 'react';
import { FlatList, Platform, StyleSheet, Text } from 'react-native';
// only renders to areas of the screen that are in view, so no need for padding in search bar
import { SafeAreaView } from 'react-native-safe-area-context';
import PlaceCard from '../components/placecards';


const API_URL = 'http://127.0.0.1:5000';


export default function Index(){
    const [search, setSearch] = useState("");
    const [searchQuery, setSearchQuery] = useState("");
    const [places, setPlaces] = useState([]);


    const updateSearch = (search: SetStateAction<string>) => {
        setSearch(search);
    };

    const makeQuery = (e: { nativeEvent: { text: any; }; }) => {
        const submittedText = e.nativeEvent.text;
        setSearchQuery(submittedText);
    }

    const [location, setLocation] = useState<Location.LocationObject | null>(null);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);

    // fetch from backend
    useFocusEffect(
        useCallback(() => {
            let url = `${API_URL}/places`;
            if (location) {
                url += `?lat=${location.coords.latitude}&lng=${location.coords.longitude}`;
            }
            if (search && !location) {
                url += `?name=${searchQuery}`;
            }
            else {
                url += `&name=${searchQuery}`;
            }
            fetch(url)
                .then(response => response.json())
                .then(data => setPlaces(data))
                .catch(error => console.error('Error fetching places:', error));
        }, [location,searchQuery])  // re-runs when location loads
    );

    // gets location data
    useEffect(() => {
        async function getCurrentLocation() {
        
        let { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
            setErrorMsg('Permission to access location was denied');
            return;
        }

        let location = await Location.getCurrentPositionAsync({});
        setLocation(location);
        }

        getCurrentLocation();
    }, []);

    let text = 'Waiting...';
    if (errorMsg) {
        text = errorMsg;
    } else if (location) {
        text = `Latitude: ${location.coords.latitude}, Longitude: ${location.coords.longitude}`;
    }

    const handlePlacePress = (placeId: string) => {
        console.log('Place pressed:', placeId);
    };

    const renderPlaceCard = ({ item }: any) => (
        <PlaceCard
            id={item.id}
            name={item.name}
            rating={item.rating}
            priceLevel={item.priceLevel}
            onPress={() => handlePlacePress(item.id)}
        />
    );


    return(
        <SafeAreaView style={styles.container}>
            <SearchBar
                platform = {Platform.OS == 'ios' ? 'ios' : 
                           (Platform.OS == 'android' ? 'android' : 'default')} // makes search work on ios and android
                placeholder="Type Here..."
                onChangeText={updateSearch}
                value={search}
                onSubmitEditing={makeQuery}
                
                // Styles
                containerStyle={styles.searchContainer}
                inputContainerStyle={styles.searchInputContainer}
                inputStyle={styles.searchInput}
                placeholderTextColor="#888"
            />
            <Text style={styles.content}>Explore</Text>
            <FlatList
                data={places}
                renderItem={renderPlaceCard}
                keyExtractor={(item) => item.id}
                contentContainerStyle={styles.listContent}
                showsVerticalScrollIndicator={false}
            />
            <Text>{searchQuery}</Text>
            <Text>{text}</Text>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        
    },
    content:{   
        flex: 1,
        justifyContent: 'center',
        fontSize: 20,
        fontWeight: 'bold',
    },
    searchContainer: {
        backgroundColor: 'transparent', // Removes default gray background
        borderTopWidth: 0, // Removes top border line
        borderBottomWidth: 0, // Removes bottom border line
        paddingTop: 0, // Removes default padding
    },
    searchInputContainer: {
        backgroundColor: '#f2f2f2', // Light gray box
        borderRadius: 20, // Rounded corners (make it 0 for square)
        height: 45,
    },
    searchInput: {
        color: '#000', // Text color
        fontSize: 16,
    },
    listContent: {
        paddingVertical: 6,
    },

});