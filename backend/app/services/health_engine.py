def score(w):
 t=w.get('temperature');h=w.get('humidity');
 s=100
 if t is None:return {'ecosystem_health':50,'risk':'Unknown'}
 if t>35:s-=20
 if h<30:s-=10
 return {'ecosystem_health':s,'risk':'Low' if s>=80 else 'Medium' if s>=60 else 'High'}
