<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>maxwvel_style</sld:Name>
    <sld:UserStyle>
      <sld:Name>maxwvel_style</sld:Name>
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
                <sld:ColorMapEntry color="#331317" quantity="0.0" label=".0 m"/>
                <sld:ColorMapEntry color="#561E22" quantity="1.0" label="1.0 m"/>
                <sld:ColorMapEntry color="#7A2923" quantity="2.0" label="2.0 m"/>
                <sld:ColorMapEntry color="#973B1C" quantity="3.0" label="3.0 m"/>
                <sld:ColorMapEntry color="#AD5515" quantity="4.0" label="4.0 m"/>
                <sld:ColorMapEntry color="#BE7313" quantity="5.0" label="5.0 m"/>
                <sld:ColorMapEntry color="#CC9219" quantity="6.0" label="6.0 m"/>
                <sld:ColorMapEntry color="#D6B427" quantity="7.0" label="7.0 m"/>
                <sld:ColorMapEntry color="#DED738" quantity="8.0" label="8.0 m"/>
                <sld:ColorMapEntry color="#E1FE4B" quantity="9.0" label="9.0 m"/>
            </sld:ColorMap>
            <sld:ContrastEnhancement/>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>