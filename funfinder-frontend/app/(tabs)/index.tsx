import { Text, StyleSheet, Platform } from 'react-native';
import { SearchBar } from '@rneui/themed';
import { SetStateAction, useState } from 'react';

// only renders to areas of the screen that are in view, so no need for padding in search bar
import { SafeAreaView } from 'react-native-safe-area-context';


export default function Index(){
    const [search, setSearch] = useState("");

    const updateSearch = (search: SetStateAction<string>) => {
    setSearch(search);
    };

    return(
        <SafeAreaView style={styles.container}>
            <SearchBar
                platform = {Platform.OS == 'ios' ? 'ios' : (Platform.OS == 'android' ? 'android' : 'default')}
                placeholder="Type Here..."
                onChangeText={updateSearch}
                value={search}
                
                // Styles
                containerStyle={styles.searchContainer}
                inputContainerStyle={styles.searchInputContainer}
                inputStyle={styles.searchInput}
                placeholderTextColor="#888"
            />
            <Text style={styles.content}>Home Screen</Text>
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