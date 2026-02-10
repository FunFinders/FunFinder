import { View, Text, StyleSheet } from 'react-native';
import { SearchBar } from '@rneui/themed';
import { SetStateAction, useState } from 'react';


export default function Index(){
    const [search, setSearch] = useState("");

    const updateSearch = (search: SetStateAction<string>) => {
    setSearch(search);
    };

    return(
        <View style={styles.container}>
            <SearchBar
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
        </View>
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
        flex: 1,
        justifyContent: "flex-start",
        backgroundColor: 'transparent', // Removes default gray background
        borderTopWidth: 0, // Removes top border line
        borderBottomWidth: 0, // Removes bottom border line
        paddingTop: 50, // Removes default padding
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