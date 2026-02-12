import { Text, StyleSheet, Platform } from 'react-native';
import { SearchBar } from '@rneui/themed';
import { SetStateAction, useState, useEffect } from 'react';
import * as Location from 'expo-location';
// only renders to areas of the screen that are in view, so no need for padding in search bar
import { SafeAreaView } from 'react-native-safe-area-context';


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
            <Text style={styles.content}>Home Screen</Text>
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

});