import matplotlib.pyplot as plt
import seaborn as sns

def plot_projections(x, y, show_points=True, weighting=False):
	
	sns.kdeplot(x=x, y=y, fill=True)
	
	if show_points == True:
		plt.scatter(x, y, label='data', c='darkorange', alpha=0.7)

	plt.gca().set_aspect('equal', adjustable='box')

	plt.show()
