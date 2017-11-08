{% extends 'gis/admin/openlayers.js' %}


{% block base_layer %}
    {{ module }}.layers.base = new OpenLayers.Layer.Bing({
        key: "{{ bing_key|safe }}",
        type: "Road"
    });
{% endblock base_layer %}

{% block controls %}
    {% if not wkt %}
       // 'Re-center' map on Portland if Point is not defined
        {{ module }}.map.setCenter(
            new OpenLayers.LonLat(
                {{ default_lon }}, {{ default_lat }}
            ).transform(
                 new OpenLayers.Projection("EPSG:4326"),
                 new OpenLayers.Projection("EPSG:3857")
            ),
            {{ default_zoom }}
        );
    {% endif %}
    {{ block.super }}
{% endblock controls %}
