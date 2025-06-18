Весь код писал в shop (не был уверен куда стоит поместить). 
Добавил модель, сериализатор для Ревью.
В представлении определил get, post, patch, delete
В shop/models/Product добавил метод average_rating, после чего интегрировал его в сериализатор через SerializerMethodField()
