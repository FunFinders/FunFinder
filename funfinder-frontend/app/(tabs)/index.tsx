import { Text, StyleSheet, Platform, FlatList } from 'react-native';
import { SearchBar } from '@rneui/themed';
import { SetStateAction, useState, useEffect } from 'react';
import * as Location from 'expo-location';
// only renders to areas of the screen that are in view, so no need for padding in search bar
import { SafeAreaView } from 'react-native-safe-area-context';
import PlaceCard from '../components/placecards';


const test_places = [
{
    id: '1',
    name: 'Sushi Place',
    rating: 4.5,
    priceLevel: 3,
},
{
    id: '2',
    name: 'Pizza Place',
    rating: 4.0,
    priceLevel: 2,
},
{
    id: '3',
    name: 'Burger Place',
    rating: 3.5,
    priceLevel: 1,
},
{  
    id: '4',
    name: 'Fancy Shmancy',
    rating: 4.8,
    priceLevel: 4,
}
];



export default function Index(){
    const [search, setSearch] = useState("");
    const [test, setText] = useState("Search something to change this text!!");

    const updateSearch = (search: SetStateAction<string>) => {
        setSearch(search);
    };

    const updateText = (e: { nativeEvent: { text: any; }; }) => {
        const submittedText = e.nativeEvent.text;
        setText(submittedText);
    }

    const [location, setLocation] = useState<Location.LocationObject | null>(null);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);

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

    const renderPlaceCard = ({ item }: { item: typeof test_places[0] }) => (
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
                onSubmitEditing={updateText}
                
                // Styles
                containerStyle={styles.searchContainer}
                inputContainerStyle={styles.searchInputContainer}
                inputStyle={styles.searchInput}
                placeholderTextColor="#888"
            />
            <Text style={styles.content}>Explore</Text>
            <FlatList
                data={test_places}
                renderItem={renderPlaceCard}
                keyExtractor={(item) => item.id}
                contentContainerStyle={styles.listContent}
                showsVerticalScrollIndicator={false}
            />
            <Text>{test}</Text>
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