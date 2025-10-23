(function($) {
    $(document).ready(function() {
        var roomSelect = $('#id_room_or_Product_Type');
        var productSelect = $('#id_Product_Type');
        var subProductSelect = $('#id_Sub_Product');

        // Store all original options
        var productOptions = productSelect.find('option').clone();
        var subProductOptions = subProductSelect.find('option').clone();

        function filterProductTypes() {
            var roomVal = roomSelect.val();
            productSelect.empty();
            productSelect.append('<option value="">---------</option>');
            productOptions.each(function() {
                if ($(this).data('room') == roomVal || $(this).val() == "") {
                    productSelect.append($(this));
                }
            });
            productSelect.trigger('change');
        }

        function filterSubProducts() {
            var productVal = productSelect.val();
            subProductSelect.empty();
            subProductSelect.append('<option value="">---------</option>');
            subProductOptions.each(function() {
                if ($(this).data('product') == productVal || $(this).val() == "") {
                    subProductSelect.append($(this));
                }
            });
        }

        roomSelect.change(filterProductTypes);
        productSelect.change(filterSubProducts);

        // Trigger initial filtering
        filterProductTypes();
        filterSubProducts();
    });
})(django.jQuery);
