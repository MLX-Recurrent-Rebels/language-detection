import torch
import dataset
import pandas
import model


data = pandas.read_parquet('/home/dataset/Flores7Lang.parquet')
ds = dataset.LangData(data)
dl = torch.utils.data.DataLoader(ds, batch_size=1, shuffle=True)


vocab_size = len(ds.tknz.vocab)
loaded_embeddings = torch.load('cbow_epoch_3.pt')
loaded_embeddings = loaded_embeddings['embeddings.weight']
lang = model.Language(loaded_embeddings, 7)
loss_function = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(lang.parameters(), lr=0.001)
torch.save(lang.state_dict(), f"./lang_epoch_0.pt")


for epoch in range(5):
  for sentence, target, _ in dl:
    optimizer.zero_grad()
    log_probs = lang(sentence)
    loss = loss_function(log_probs, target)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}/5, Loss: {loss.item()}")
  torch.save(lang.state_dict(), f"./lang_epoch_{epoch+1}.pt")