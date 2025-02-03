import React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import HomeScreen from './modules/Home/HomeScreen';

function App() {
  return (
    <View style={styles.container}>
      {/* <Text>Hello Simform</Text> */}
      <HomeScreen />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default App;
