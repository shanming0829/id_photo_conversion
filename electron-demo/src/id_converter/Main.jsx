import React, { useState } from 'react';
import Container from 'react-bootstrap/Container';
import ConditionView from './ConditionView.jsx';
import ImageView from './ImageView.jsx';


const Main = () => {
  const [image, setImage] = useState(null)

  return (
    <Container>
      <ConditionView onConvertedImage={setImage}/>
      <ImageView image={image}/>
    </Container>
  )
}

export default Main
