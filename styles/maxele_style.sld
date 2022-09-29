<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>maxele_style</sld:Name>
    <sld:UserStyle>
      <sld:Name>maxele_style</sld:Name>
      <sld:FeatureTypeStyle>
        <sld:Name>name</sld:Name>
        <sld:Rule>
          <sld:RasterSymbolizer>
            <sld:ChannelSelection>
              <sld:GrayChannel>
                <sld:SourceChannelName>1</sld:SourceChannelName>
                <sld:ContrastEnhancement>
                  <sld:GammaValue>1.0</sld:GammaValue>
                </sld:ContrastEnhancement>
              </sld:GrayChannel>
            </sld:ChannelSelection>
            <sld:ColorMap type="ramp">
              <sld:ColorMapEntry color="#00005F" quantity="0.0" label="0.0 m"/>
              <sld:ColorMapEntry color="#005FFF" quantity="0.5" label="0.5 m"/>
              <sld:ColorMapEntry color="#00BFFF" quantity="1.0" label="1.0 m"/>
              <sld:ColorMapEntry color="#5FFF9F" quantity="2.0" label="2.0 m"/>
              <sld:ColorMapEntry color="#FFDF00" quantity="3.0" label="3.0 m"/>
              <sld:ColorMapEntry color="#FF3F00" quantity="4.0" label="4.0 m"/>
              <sld:ColorMapEntry color="#9F0000" quantity="5.0" label="5.0 m"/>
              <sld:ColorMapEntry color="#7F0000" quantity="6.0" label="6.0 m"/>
            </sld:ColorMap>
            <sld:ContrastEnhancement/>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>