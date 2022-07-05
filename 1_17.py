v1 = [x for x in range(1, 4)]
print(v1)

v2 = [y for y in range(4, 7)]
print(v2)

print('Produto escalar dos vetores', v1, ' e ', v2,
      'é: ', sum(x_i*y_i for x_i, y_i in zip(v1, v2)))
