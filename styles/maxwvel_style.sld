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
                <sld:ColorMapEntry color="#29186C" quantity="0.0" label="0.0 m/s"/>
                <sld:ColorMapEntry color="#242DA3" quantity="2.0" label="2.0 m/s"/>
                <sld:ColorMapEntry color="#0C5493" quantity="4.0" label="4.0 m/s"/>
                <sld:ColorMapEntry color="#206E8B" quantity="6.0" label="6.0 m/s"/>
                <sld:ColorMapEntry color="#348688" quantity="8.0" label="8.0 m/s"/>
                <sld:ColorMapEntry color="#43A085" quantity="10.0" label="10.0 m/s"/>
                <sld:ColorMapEntry color="#59BA78" quantity="12.0" label="12.0 m/s"/>
                <sld:ColorMapEntry color="#87D061" quantity="14.0" label="14.0 m/s"/>
                <sld:ColorMapEntry color="#CADF68" quantity="16.0" label="16.0 m/s"/>
                <sld:ColorMapEntry color="#FEEF9A" quantity="18.0" label="18.0 m/s"/>
            </sld:ColorMap>
            <sld:ContrastEnhancement/>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>