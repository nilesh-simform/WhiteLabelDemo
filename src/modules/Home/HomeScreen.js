import React from 'react';
import {Text, View} from 'react-native';
import HomeStyles from './HomeStyles';

const HomeScreen = () => {
  return (
    <View style={HomeStyles.containerStyle}>
      <Text style={HomeStyles.textStyle}>Hello Simform</Text>
    </View>
  );
};

export default HomeScreen;
