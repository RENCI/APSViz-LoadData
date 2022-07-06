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
                <sld:ColorMapEntry color="#29186C" quantity="0.0" label="0.0 m"/>
                <sld:ColorMapEntry color="#2E1B8B" quantity="1.0" label="1.0 m"/>
                <sld:ColorMapEntry color="#2828A2" quantity="2.0" label="2.0 m"/>
                <sld:ColorMapEntry color="#173D9E" quantity="3.0" label="3.0 m"/>
                <sld:ColorMapEntry color="#0D4E96" quantity="4.0" label="4.0 m"/>
                <sld:ColorMapEntry color="#0F5B90" quantity="5.0" label="5.0 m"/>
                <sld:ColorMapEntry color="#18668C" quantity="6.0" label="6.0 m"/>
                <sld:ColorMapEntry color="#23728A" quantity="7.0" label="7.0 m"/>
                <sld:ColorMapEntry color="#2C7C89" quantity="8.0" label="8.0 m"/>
                <sld:ColorMapEntry color="#348788" quantity="9.0" label="9.0 m"/>
                <sld:ColorMapEntry color="#3B9387" quantity="10.0" label="10.0 m"/>
                <sld:ColorMapEntry color="#429E85" quantity="11.0" label="11.0 m"/>
                <sld:ColorMapEntry color="#4AAA81" quantity="12.0" label="12.0 m"/>
                <sld:ColorMapEntry color="#55B67B" quantity="13.0" label="13.0 m"/>
                <sld:ColorMapEntry color="#64C172" quantity="14.0" label="14.0 m"/>
                <sld:ColorMapEntry color="#79CB67" quantity="15.0" label="15.0 m"/>
                <sld:ColorMapEntry color="#94D45D" quantity="16.0" label="16.0 m"/>
                <sld:ColorMapEntry color="#B3DA5E" quantity="17.0" label="17.0 m"/>
                <sld:ColorMapEntry color="#CFE06C" quantity="18.0" label="18.0 m"/>
                <sld:ColorMapEntry color="#E8E782" quantity="19.0" label="19.0 m"/>
                <sld:ColorMapEntry color="#FEEF9A" quantity="20.0" label="20.0 m"/>
            </sld:ColorMap>
            <sld:ContrastEnhancement/>
          </sld:RasterSymbolizer>
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>