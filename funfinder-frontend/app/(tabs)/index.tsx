import { View, Text, StyleSheet } from 'react-native';

export default function Index(){
    return(
        <View style={styles.container}>
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
        fontSize: 20,
        fontWeight: 'bold',
    }


});