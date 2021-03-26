import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Image from 'react-bootstrap/Image';

const ImageView = ({image}) => {
  return (
    <Row>
      <Col>
        {image && <Image src={image} fluid />}
      </Col>
    </Row>
  )
}

export default ImageView